# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 11141  GET              /                                                dashboard
 13198  GET              /api/abo/status                                  api_abo_status
 13152  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11929  GET              /api/automation/status                           api_automation_status
 11951  POST             /api/automation/toggle                           api_automation_toggle
 21779  GET              /api/channel/categories                          api_channel_categories
 21785  POST             /api/channel/set                                 api_channel_set
 21632  GET              /api/channels/status                             api_channels_status
 21306  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21289  GET              /api/clips                                       api_clips
 21335  POST/DELETE      /api/clips/clear                                 api_clips_clear
 21207  GET              /api/debug/threads                               api_debug_threads
 13163  GET              /api/events                                      api_events
 12642  GET              /api/events/stream                               api_events_stream
 12469  GET              /api/health                                      api_health
 21248  POST             /api/highlights/config                           api_highlights_config
 11071  POST             /api/login                                       dashboard_login_submit
 13488  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 12557  GET              /api/notify/status                               api_notify_status
 12568  POST             /api/notify/test                                 api_notify_test
 13252  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13229  GET              /api/proxy/trend                                 api_proxy_trend
 21355  GET              /api/tts/<fn>                                    api_tts_file
 22129  GET              /api/upload_window                               api_upload_window
 12759  GET              /archive/<int:eid>/download                      archive_download
 12787  GET              /download/<int:recording_id>                     download
 12716  GET              /health                                          health
 21093  GET              /healthz                                         healthz
 11062  GET              /login                                           dashboard_login_page
 11096  GET              /logout                                          dashboard_logout
 11103  GET              /manifest.webmanifest                            pwa_manifest
 22102  GET              /overlay                                         overlay_page
 11127  GET              /pwa-icon-<variant>.png                          pwa_icon
 11113  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (345)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   997  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   868  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   848  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   886  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1235  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1267  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   950  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   930  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1103  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1151  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1202  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1061  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   905  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   504  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   768  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   650  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   633  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   625  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   812  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   777  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   797  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   684  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   238  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   263  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   268  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   417  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   408  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   343  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   230  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   196  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   179  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   532  GET              /api/beobachtung/dienste                         api_beobachtung_dienste   [nc/routes/beobachtung.py]
   525  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
   547  POST             /api/beobachtung/steuern                         api_beobachtung_steuern   [nc/routes/beobachtung.py]
   376  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   198  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   131  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   116  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    93  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   158  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    80  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    81  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    53  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   174  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    40  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    52  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    52  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    87  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   122  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   443  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   439  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   424  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   244  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   265  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   292  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   385  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   329  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   347  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   252  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   164  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   125  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   146  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    91  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   244  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   170  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   188  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   160  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    63  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   136  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    79  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   125  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   139  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   154  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
    56  GET              /api/einstellungen                               api_einstellungen   [nc/routes/einstellungen.py]
    68  POST             /api/einstellungen                               api_einstellungen_setzen   [nc/routes/einstellungen.py]
   102  POST             /api/einstellungen/uebernehmen                   api_einstellungen_uebernehmen   [nc/routes/einstellungen.py]
    86  POST             /api/einstellungen/zuruecksetzen                 api_einstellungen_zuruecksetzen   [nc/routes/einstellungen.py]
   194  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   179  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    90  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   112  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   133  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
   150  POST             /api/evolution/proposals/bulk                    api_evolution_bulk   [nc/routes/evolution.py]
    80  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   209  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    44  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   222  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   242  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   269  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   394  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   297  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   414  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   409  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   485  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   307  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   168  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    43  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   150  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   125  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   189  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    76  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    99  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   223  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   225  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   247  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   174  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   131  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   181  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   119  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   167  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   184  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   215  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   191  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   251  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   221  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    82  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   235  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
    66  GET              /api/lagebild                                    api_lagebild   [nc/routes/lagebild.py]
   428  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    78  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
   103  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   113  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    52  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    70  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   225  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
   100  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    66  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    77  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   142  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   137  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   128  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    53  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    92  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   257  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   324  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   352  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   203  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   270  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   505  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    80  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   168  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   151  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   391  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   238  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   229  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   212  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
   121  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   268  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   590  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   565  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   974  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1096  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1124  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1144  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   961  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1023  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1010  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   991  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   636  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   631  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   679  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   562  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   889  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   653  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   616  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   589  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   863  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   733  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   822  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   728  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   661  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   441  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   906  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   529  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   784  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   939  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   924  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   485  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   723  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   709  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   692  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   749  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1287  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1408  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1251  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   842  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   738  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   522  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   539  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   591  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   613  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   552  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   578  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   148  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   160  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   480  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   470  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   505  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    65  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    86  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    52  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
   102  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   366  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
    92  GET              /api/selftest                                    api_selftest   [nc/routes/selbsttest.py]
   456  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   128  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   219  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   214  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   274  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   578  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   397  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   427  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   126  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   273  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    88  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   298  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   230  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   254  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   185  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   150  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   210  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    56  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   219  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
    74  GET              /api/system                                      api_system   [nc/routes/systemlage.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   178  GET              /api/system/check_timing                         api_check_timing   [nc/routes/systemlage.py]
   118  GET              /api/system/config_drift                         api_config_drift   [nc/routes/systemlage.py]
   141  GET              /api/system/config_snapshot                      api_system_config_snapshot   [nc/routes/systemlage.py]
   238  GET              /api/system/preflight                            api_system_preflight   [nc/routes/systemlage.py]
   105  GET              /api/system/preflight_history                    api_system_preflight_history   [nc/routes/systemlage.py]
   375  GET              /api/system/resilience                           api_system_resilience   [nc/routes/systemlage.py]
   389  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   189  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   237  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   458  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   487  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   407  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   420  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   516  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   393  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   268  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   337  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   324  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   164  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   282  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   133  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   374  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   429  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   265  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   121  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
   100  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   132  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   113  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   125  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    77  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
   101  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    55  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   453  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   419  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   478  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   458  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   441  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   434  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   251  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   317  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    52  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    92  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   123  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
   107  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   131  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   152  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   164  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    89  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   113  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    67  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   199  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
    73  GET              /fonts/<name>                                    schrift   [nc/routes/schriften.py]
    66  GET              /fonts/schriften.css                             schriften_css   [nc/routes/schriften.py]
   469  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (67)

```
  2276  /about                  Ueber diesen Bot
   980  /ai                     
  2276  /aireset                KI-Kontext zuruecksetzen
  1395  /ask                    
  1081  /assign_role            
  1131  /ban                    
  2231  /botstats               
  2276  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2276  /bulkadd                Mehrere User auf einmal tracken · a b c
  2276  /cleanup                Alte Aufnahmen aufraeumen
  1661  /clearwarns             
  2195  /clip                   
  2180  /clipoftheweek          
  1531  /clips                  
  2276  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
  1036  /create_category        
  1007  /create_channel         
  1071  /create_group           
  1046  /create_role            
  1022  /create_voice           
  1272  /daily                  
  2276  /diag                   Vollstaendige Diagnose
  2276  /einnahmen              Einnahmen und Spenden
  1424  /event                  
  1466  /events                 
  1571  /follow                 
  1560  /help                   
  1121  /kick                   
  1247  /leaderboard            
  2276  /live                   Live-Status sofort pruefen · @user
  1518  /livenow                
  2276  /logs                   Letzte Fehler aus dem Log
  2276  /pause                  Tracking pausieren · @user
  1546  /post_test              
  1356  /profile                
  1153  /purge                  
  2276  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2276  /quota                  Speicher-Quota
  1234  /rank                   
  1506  /recstatus              
  1091  /remove_role            
  2276  /report                 Azrael-Sentinel-Wochenreport
   993  /restream_status        
  2276  /resume                 Tracking fortsetzen · @user
  1101  /set_channel_perms      
  1196  /setup_community        
  1213  /setup_targets          
  1492  /spenden                
  1603  /stats                  
   952  /status                 
  2276  /stoprec                Laufende Aufnahme sauber beenden · @user
  1699  /streaminfo             
  2276  /summary                Tageszusammenfassung
  2276  /sysres                 System-Ressourcen
  2276  /teststream             Recorder-Selbsttest · @user
  2276  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
  1141  /timeout                
  1671  /topstreamers           
  2276  /topusers               Top-Streamer nach Aufnahmen
   882  /track                  
  2276  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   965  /tracklist              
  1585  /unfollow               
  2276  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   914  /untrack                
  1624  /warn                   
  1647  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2443  on_member_join
  2400  on_message
  2297  on_raw_reaction_add
  2478  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    60-75     konfiguriere
    78-533    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (54 Funktionen)

```
  1776-1827   _award_xp
   536-563    _bereich_umziehen
   483-493    _clip_kopieren
  1998-2027   _clip_week_leader
  2051-2065   _clipoftheweek_loop
  2595-2657   _community_events_loop
  1733-1755   _dc_client
  1758-1767   _dc_offen
  2697-2732   _disc_automod_check
   409-414    _disc_sprache_setzen
  1830-1878   _discord_ai_automod
   685-724    _discord_automod
  1881-1901   _discord_azrael_reply
  2068-2554   _discord_run_once
   244-302    _discord_start
   305-359    _ensure_discord_invite
  2560-2592   _ensure_error_channel
   430-443    _ensure_rank_roles
   845-859    _ensure_team_roles
  2660-2690   _error_channel_loop
   734-738    _guard
   654-682    _handle_voice_ai
   417-427    _is_admin
   508-533    _link_video
  1946-1957   _liveboard_loop
   741-774    _on_level_up
   650-651    _par_chat_id
  2030-2048   _post_clip_of_week
  1960-1978   _post_weekly_digest
   446-472    _provision_base_channels
  1498-1592   _reg_betrieb
  1167-1261   _reg_community_setup
  1264-1345   _reg_daily_profil
  1388-1485   _reg_frage_events
   939-995    _reg_info
  1113-1164   _reg_moderation
  1348-1385   _reg_profil
  1062-1110   _reg_rollen
   998-1059   _reg_server
  1488-1495   _reg_spenden
  1595-1682   _reg_streamer
  1685-1730   _reg_system
   873-936    _reg_tracking
   809-842    _run_tg_handler
   637-647    _tracked_usernames
   161-223    _uebernehmen
   496-505    _umzugsmarken
  1910-1943   _update_liveboard
  1981-1995   _weekly_digest_loop
   475-480    _ziel_guild
   566-608    _ziele_abgleichen
   617-634    _ziele_sync_loop
   611-614    _ziele_takt_min
   226-229    starte
```

## Top-Level-Symbole in bot.py (605 Funktionen, 4 Klassen)

```
 27273-27295  _abbruch_datenbank_unlesbar
  2836-2837   _abo_key
  2857-2875   _abo_probe_dump
 27391-27407  _abschied_wachen
 27410-27428  _abschluss
 17361-17368  _ad_allowlist
 18523-18529  _agent_for
 18532-18548  _ai_telemetry
 19045-19063  _alert
 22997-23047  _alert_monitor_loop
 19739-19796  _alte_beilagen_einsammeln
 23429-23491  _announce_loop
  3736-3746   _anthropic_key
  3753-3755   _anthropic_model
 10630-10633  _arg_int
  2828-2833   _as_dict
 26959-26968  _async_exc_handler
 19233-19255  _audio_tap_cmd
 20259-20318  _audio_tap_melden
 19269-19293  _audio_tap_sammler
  9976-10013  _aufnahme_beim_stopp_sichern
 19681-19702  _aufnahme_chat_ausklang
 19665-19678  _aufnahme_chat_beginnen
 19824-19845  _aufnahme_chat_dienst
 20018-20071  _aufnahme_chat_einarbeiten
 19660-19662  _aufnahme_chat_modus
 19848-19897  _aufnahme_chat_nachtrag
 19705-19736  _aufnahme_chat_vormerken
 19815-19821  _aufnahme_chat_wecken
 26128-26130  _aufnahme_deckel
 19900-19921  _aufnahme_fertigmachen
 23666-23719  _aufnahme_nach_discord
 10016-10034  _aufnahme_platz_frei
  9919-9946   _aufnahme_verteilen
 27355-27375  _aufnahmen_abschliessen
 27298-27352  _aufraeumen
 10904-10973  _auth_cookie
 10860-10900  _auth_guard
  2063-2068   _auto_on
 20945-20963  _auto_restream_loop
 14833-14875  _avatar_frames_laden
 17411-17424  _azrael_brain_kontext
 24625-24640  _azrael_broadcast_reply
 24525-24547  _azrael_chat_reply
 24497-24522  _azrael_chat_should_reply
 24553-24555  _azrael_gate_cfg
 18553-18567  _azrael_live_state
 22015-22029  _azrael_overlay_state
 18927-18981  _azrael_proactive_loop
 18371-18427  _azrael_reaction_to_chats
 24558-24565  _azrael_reply_all_chats
 24484-24494  _azrael_self_names
 24593-24622  _azrael_send_to
 14794-14830  _azrael_spricht
 15141-15154  _azrael_stimme_stumm
 18573-18594  _azrael_system
 23131-23134  _backup_active
 23212-23225  _backup_loop
  5494-5517   _betreiber_pruefen
 26217-26221  _betrieb
 27032-27041  _brain_crowdsec_snap
 27200-27203  _brain_db_health
 22918-22927  _brain_growth_loop
 11320-11347  _brain_growth_snapshot
  2747-2781   _brain_hint_delay
 27104-27139  _brain_moderation_snap
  6768-6796   _brain_notify
 27206-27228  _brain_recording_snap
 27044-27101  _brain_restream_health
 27231-27244  _brain_tiktok_status_snap
 12621-12638  _browser_push
  6808-6895   _build_daily_summary
 15188-15192  _build_restream_cmd
  5520-5547   _can_stop_tracking
  2176-2198   _capture_set_cookies
 13306-13309  _cfg_get
 13312-13314  _cfg_set
 21740-21775  _channel_set_all
 13885-13888  _chat_connected
 13891-13907  _chat_disconnected
 19809-19812  _chat_einarbeiten_async
  9414-9444   _chat_is_forum
 19629-19654  _chat_listener_abbauen
  9586-9621   _chat_migriert
  9624-9625   _chat_migriert_async
 13927-13929  _chat_sanitize
 13870-13882  _chat_stat
 13910-13913  _chat_stats_snapshot
  4059-4071   _check_ai_models_sync
 11602-11645  _classify_pool_anonymity
 11648-11665  _classify_pool_anonymity_bg
   911-933    _claude_chat_sync_metered
 10662-10668  _client_ip
 24124-24138  _clip_chat_ass
 23575-23609  _clip_prune
 23612-23622  _clip_recfile_for
 24044-24112  _clip_schneiden
 24141-24147  _clip_should_velocity
 23722-23807  _clip_to_discord
 19989-19994  _clips_abwarten
  3940-3949   _close_ai_session
 24671-24686  _cohost_broadcast
 24656-24657  _cohost_cfg
 24712-24724  _cohost_fire_highlight
 24660-24668  _cohost_gate
 24689-24709  _cohost_highlight
 11250-11252  _conv_messages
  7192-7253   _cookie_alarm_loop
  2266-2267   _cookie_autofetch_info
  2250-2254   _cookie_autorefresh_info
 26666-26688  _cookie_bezug_loop
 26691-26716  _cookie_bezug_runde
  2153-2157   _cookie_header
 10671-10676  _cookie_sicher
  2279-2293   _cookies_selbst_holen
  4280-4282   _create_index_safe
 22461-22575  _crowdsec_status
 22407-22458  _crowdsec_via_lapi
 22311-22329  _cscli_bin
 22338-22351  _cscli_path
  7076-7103   _daily_summary_loop
 22369-22386  _darf_journal_lesen
  3261-3286   _darf_ytdlp_nachschlagen
 12802-12823  _dashboard_adresse
 10691-10695  _dashboard_hostnamen
  1515-1545   _dashboard_trackings_umziehen
 24115-24121  _datei_weg
 22971-22994  _db_maintenance_loop
  7026-7073   _db_vacuum_loop
 17384-17408  _detect_foreign_ad
  1743-1754   _diag_path_owner
 18832-18877  _director_finalize
 20248-20255  _director_for
 18781-18829  _director_mark
 23957-23960  _disc_state_get
 23963-23970  _disc_state_set
 22899-22908  _discord_bot_starten
 22862-22873  _discord_einladung_merken
 22911-22915  _discord_invite
 22876-22896  _discord_kontext
 23918-23954  _discord_live_thread
 18984-18996  _discord_notify
 22834-22859  _discord_ops_alert
 23818-23914  _discord_post_user
 23494-23500  _discord_stop
  7106-7187   _disk_alarm_loop
 26537-26588  _disk_autoclean
 26814-26827  _disk_guard_loop
 14772-14779  _drossel_hoeher
 14768-14769  _drossel_stufe
 14782-14790  _drossel_zuruecksetzen
 12979-12981  _dump_all_threads
 26224-26238  _einstellungen_startzeile
 11528-11591  _enrich_proxies_with_geo
  2322-2383   _ensure_cookie_file_netscape
  9515-9518   _ensure_notify_topic
 11772-11809  _ensure_proxy_ready
  9454-9477   _ensure_topic
   752-754    _env_int
   757-759    _env_int_range
 19029-19042  _event_webhook
 13653-13666  _evolution_loop
  6209-6243   _extract_file_payload
  2455-2457   _extract_urls_from_streamurl_node
 22354-22361  _f2b_sudo_hint
  1501-1512   _fanout_ziele
 27431-27494  _fatal_vom_botteil
 26133-26148  _fd_grenze_anheben
  4954-4964   _fehler_text
 11429-11447  _fetch_proxy_list
 19598-19626  _fetch_tiktok_room_id
   837-840    _ff_cmd
 20002-20015  _ffprobe_masse
 14716-14732  _fifo_schreiber_wecken
 14526-14531  _find_chromium
  3656-3658   _find_external_recorder
  2460-2462   _find_stream_urls
 13357-13382  _fire_webhooks
  8076-8086   _fork_safe
   944-957    _freeai_chat_sync_metered
 22400-22404  _geo_lookup_ips
  3928-3937   _get_ai_session
  7904-7944   _get_live_info
  3112-3119   _get_resolve_semaphore
  8603-9023   _handle_single_tracking
 26333-26335  _hb
 26338-26355  _hb_while
 21192-21203  _healthz_fuer_aufrufer
 26379-26395  _heap_zurueckgeben
 10977-10994  _herkunft_guard
 13941-13943  _highlight_cfg
 13946-13975  _highlight_observe
 14577-14585  _htmlov_bild_schreiben
 14555-14574  _htmlov_dauerbrowser
 14534-14552  _htmlov_screenshot_cmd
 19295-19305  _httpx_proxy
 13390-13402  _in_quiet_hours
 27259-27270  _init_db_oder_abbruch
 28081-28112  _install_fast_eventloop
 10525-10579  _install_fast_json
 12984-13000  _install_faulthandler
 20996-21005  _intel_ensure_schema
 21048-21083  _intel_index_loop
 21017-21032  _intel_index_one
 21008-21014  _intel_semantic
  5479-5492   _is_authorized
  8429-8450   _is_dead
  2445-2447   _is_hevc
 22389-22391  _is_private_ip
  1962-1969   _is_process_running
  6798-6805   _is_quiet_hours
  1403-1412   _is_upload_window
  4819-4834   _iso
 10679-10688  _ist_lokal
 10614-10627  _json_error_handler
  7020-7021   _kick_broadcaster_id
  8304-8311   _kick_cluster_gefunden
  8239-8301   _kick_cluster_weiter
  6932-6974   _kick_follower_count
  6916-6919   _kick_slug
 12434-12441  _kick_user_token
  8209-8236   _kick_ws_pause
 27247-27256  _kickmod_boot
  4364-4367   _kind_from_filename
 26632-26635  _lagebild_discord_aufnahme
 26645-26649  _lagebild_kick_chat
 26638-26642  _lagebild_overlay
 26652-26654  _lagebild_spendenziel
 26619-26629  _lagebild_upload
 13419-13421  _latest_popularity
  1899-1908   _laufstand
 26774-26811  _laufstand_loop
 26257-26295  _leistung_erheben
  7778-7805   _link_video_senden
  8590-8601   _live_check_frist_melden
 20654-20703  _live_react_loop
 20321-20643  _live_react_worker
  3504-3618   _live_status_aufloesen
 18430-18441  _live_transcript_push
 20645-20652  _live_users
 18880-18924  _living_title_loop
 23137-23209  _local_backup_scan
  4759-4782   _lock_update
 10596-10610  _log_5xx
 26298-26330  _log_schleuse_pruefen
   827-834    _log_sicher
 15200-15212  _looks_like_codec_err
 15195-15197  _looks_like_source_expired
  8127-8157   _loop_fehler
 13004-13013  _loop_heartbeat
 26039-26072  _loop_lag_monitor
 26086-26106  _loop_stockung_melden
 26109-26119  _loop_takt_starten
 13016-13089  _loop_watchdog_thread
 18307-18324  _loyalty_add
 18298-18304  _loyalty_get
 18327-18335  _loyalty_top
  5161-5180   _manual_status
  8452-8453   _mark_dead
 12048-12064  _marketing_loop
 24572-24590  _maybe_handle_command
 26913-26937  _maybe_hype_clip
 23544-23572  _meme_klassifizieren
 19924-19986  _meme_zusammenschnitt
  4267-4272   _migrate_columns
 24854-24865  _mod_is_exempt
 24868-24873  _mod_warn_first
 24876-24879  _mod_warn_text
 13710-13729  _modlog
 13693-13707  _modlog_schreiben
  1099-1101   _multistream_targets
  3289-3325   _nachschlag_ytdlp
  8089-8090   _nc_create_subprocess_exec
  8093-8094   _nc_create_subprocess_shell
 12371-12388  _news_loop
 13752-13754  _normalize_ingest
  2678-2695   _note_check_duration
  9509-9512   _notify_topic_name
  2882-2888   _offline_ergebnis
  3328-3351   _ohne_url_melden
 18456-18464  _oracle_memories
 18730-18764  _oracle_memorize
 18467-18480  _oracle_persona
 18449-18453  _oracle_recent_text
 14150-14151  _ov_atomic_write
 14141-14143  _ov_bar
 17287-17299  _ov_clip_text
 14146-14147  _ov_oneline
 22066-22095  _overlay_push
 14480-14523  _overlay_render_size
 13821-13825  _overlay_session_reset
 22031-22033  _overlay_src_ok
 14160-14172  _overlay_takt
 17371-17381  _own_invites
 14475-14477  _parse_size
 22583-22663  _parse_ssh_attacks
  7454-7487   _pause_resume_cmd
  2204-2248   _persist_refreshed_cookies
  2107-2139   _pick_checked_pull_proxy
 10745-10760  _pin_auth_value
 10849-10850  _pin_clear_fail
 10813-10816  _pin_global_gesperrt
 10766-10777  _pin_hmac_schluessel
 10819-10826  _pin_locked
 10829-10846  _pin_note_fail
 10780-10801  _pin_ok
 21873-21898  _piper_pick_model
 21958-22009  _piper_say
 13319-13354  _post_json_threaded
 14454-14472  _probe_video_size
  1990-2007   _proc_is_recorder
 11741-11769  _proxy_pool_refresh_loop
  2073-2104   _proxy_report_recording
  9162-9243   _pruef_runde
  9121-9159   _pruefstand_melden
 26168-26179  _pruefung_verworfen
 12969-12971  _prune_stall_dumps
 12118-12290  _public_stats
  2270-2276   _pull_proxy_still
 19000-19026  _push_notify
 11041-11043  _pwa_dir
 11498-11513  _quick_validate_proxy
 13385-13387  _quiet_hours_config
 11006-11039  _rate_guard
 18268-18274  _react_warn
  7991-8030   _reap_proc
 10698-10714  _rebinding_melden
  9849-9916   _rec_auto_abschalten
  9796-9846   _rec_frueh_getrennt
  9665-9741   _rec_kategorie_melden
  9744-9793   _rec_totstreak_fortschreiben
  2718-2740   _record_check_outcome
   822-824    _redact_stream_urls
 11668-11738  _refresh_proxy_pool
  2495-2586   _resolve_via_html
  2891-3089   _resolve_via_webcast_api_v2
  3152-3237   _resolve_via_ytdlp
 24181-24310  _resolve_youtube_ingest
  2471-2492   _resolver_stumm
 13804-13815  _restream_active_sources
 14878-15005  _restream_avatar_feeder_start
 15008-15018  _restream_avatar_feeder_stop
 20074-20212  _restream_chat_guardian
 13978-14050  _restream_chat_push
 14127-14136  _restream_chat_push_async
 27142-27197  _restream_durchreicher
 14588-14713  _restream_html_overlay_start
 14735-14755  _restream_html_overlay_stop
 13763-13786  _restream_overlay_files
 20707-20739  _restream_platform_state
 20907-20942  _restream_resume_after_restart
 14081-14098  _restream_soll_schreiben
 14101-14124  _restream_status_schreiben
 15066-15138  _restream_tts_enqueue_wav
 14416-14448  _restream_tts_feeder
 14413-14414  _restream_tts_fifo_path
 15021-15048  _restream_tts_start
 15050-15064  _restream_tts_stop
 20745-20904  _restream_verify_loop
 23102-23114  _retention_loop
 23096-23099  _retention_scan
  2839-2841   _room_is_abo
  6247-6364   _run_ai_call
 13112-13125  _run_async_from_flask
 22394-22397  _run_priv
 28069-28077  _run_selfcheck_and_exit
 23117-23128  _s3_client
  8479-8549   _safe_send
  5087-5103   _sample_net_throughput
  2784-2814   _schedule_next_check
 23050-23093  _scheduler_loop
  4275-4277   _schema_pk
 13129-13134  _scraper_session
 24882-24921  _screen_full
 12485-12522  _sec_headers
  2450-2452   _select_stream_from_data_section
 27786-28066  _selfcheck
  9521-9555   _send_live_notice
  1426-1430   _should_defer_upload
 23625-23663  _shrink_for_discord
 11046-11058  _sicheres_ziel
 22930-22968  _sicherheits_erinnerung_loop
 26834-26851  _sign_health_check
 26854-26873  _sign_health_loop
  4837-4862   _sitzung_bestimmen
  8106-8117   _spawn
 28500-28530  _spawn_from_flask
 26182-26188  _speicher_maps
 26191-26206  _speicher_pflegen
 19307-19595  _start_chat_listener
 26151-26165  _start_gesperrt
 13092-13109  _start_loop_watchdog
 12317-12366  _stats_loop
 12296-12299  _stats_output_path
 12302-12314  _stats_write
 21910-21924  _stimme_saubern
 21931-21955  _stimme_schon_gesagt
  9102-9118   _storage_cleanup_loop
 26893-26900  _story_for
  3681-3687   _stream_url_expiry
  3689-3694   _stream_url_ttl
 17334-17341  _streamer_persona_get
 23234-23386  _system_backup
 23395-23425  _system_backup_loop
 12929-12947  _task_auf_bot_schleife
 25719-25735  _telegram_befehlsmenue
  8160-8206   _telegram_polling_fehler
  1471-1498   _telegram_ziele
 11450-11489  _test_proxy
 11996-12012  _testpush_resolve_live
 19997-19999  _text_schreiben
  9573-9583   _tg_migriert_laden
  9569-9570   _tg_migriert_pfad
  8455-8476   _tg_sprache_setzen
  9383-9393   _tg_topics_load_into_mem
  9380-9381   _tg_topics_path
  9395-9402   _tg_topics_save
 10717-10727  _token_ok
  9480-9496   _topic_anlegen
  9405-9412   _topic_forget
 13405-13416  _tracking_max_duration
  4572-4586   _tracking_remove_cleanup
  4603-4615   _tracking_resume_cleanup
  1801-1824   _try_attach_file_handler
 21900-21908  _tts_cleanup
 11972-11976  _tunnel_effective
 26591-26611  _tunnel_lage
 26719-26771  _tunnel_wacht_loop
 21399-21452  _twitch_channel_status
 24924-25072  _twitch_chat_loop
 23976-23989  _twitch_clip_versuchen
 24735-24841  _twitch_eventsub_loop
  1591-1626   _upload_queue_abarbeiten
  1449-1469   _upload_queue_add
  1562-1564   _upload_queue_count
  1432-1441   _upload_queue_load
  1629-1651   _upload_queue_nachher
  1422-1424   _upload_queue_path
  1548-1552   _upload_queue_remove
  1443-1447   _upload_queue_save
  1555-1560   _upload_queue_update
  9949-9973   _upload_rest_sichern
  1566-1588   _upload_window_loop
  7964-7971   _uptime_s
 13740-13749  _url_host
  3354-3452   _url_nachschlag
   904-908    _usage_record_claude
 27007-27029  _v37_pause_source
 26971-26981  _v37_restream_restart
 26984-27004  _v37_unpause_source
  8378-8422   _verbindung_verloren
  6977-7008   _viewer_sample_loop
 10853-10856  _wants_html
  7974-7988   _warn_empty_env
 26398-26523  _watchdog_loop
 24456-24464  _wchat_thank_ok
 19068-19105  _whisper_get_model
  8065-8073   _whisper_native_section
 18255-18261  _whisper_pool
 19199-19231  _whisper_segments
 19107-19123  _whisper_stumm
 19126-19196  _whisper_transcribe
 14213-14370  _write_restream_overlay
 14175-14210  _write_restream_overlay_async
 25096-25195  _youtube_api_chat_loop
 21455-21558  _youtube_api_status
 21561-21628  _youtube_channel_status
 25198-25362  _youtube_chat_loop
 23992-24017  _youtube_clip_versuchen
 24316-24329  _youtube_restream_autoconfig
 24332-24356  _youtube_restream_autoconfig_inner
 24423-24451  _youtube_send
 21696-21737  _youtube_set_channel
 24359-24393  _yt_access_token
 24396-24411  _yt_live_chat_id
 24419-24420  _yt_sendrate_cfg
 25075-25090  _yt_timeout
  3136-3137   _ytdlp_detect_available
  3139-3150   _ytdlp_note_result
 12974-12976  _zombie_child_count
 26241-26254  _zustand_kennzahlen
  7840-7864   about
  4483-4487   add_ai_log_entry
  4400-4403   add_archive_entry
  5125-5127   add_archive_rule
  4865-4936   add_recording
  4547-4564   add_tracking
  6367-6400   ai
  4085-4171   ai_chat
  4205-4215   ai_history_append
  4217-4222   ai_history_clear
  4194-4203   ai_history_load
  4179-4192   ai_rate_limit_check
  6429-6437   aireset
 18597-18616  azrael_chat
 25367-25489  brain_cmd
  3697-3702   build_recording_cmd
  4567-4570   bulk_add_trackings
  7256-7315   bulkadd
  9246-9362   check_all_trackings
  4619-4631   claim_live_transition
 17427-18187  class KickModerator
 15215-17174  class RestreamManager
  4785-4786   class _AufnahmeLockVerloren
  8314-8375   class _KickClusterSuche
 11855-11897  classify_proxy_anonymity
  6475-6674   cleanup
  5415-5421   cleanup_old_recordings
  4810-4817   clear_recording
 24020-24041  clip_moment
  5077-5080   compute_storage_forecast
  7378-7451   cookies_cmd
  4538-4544   count_trackings_for_chat
  4470-4481   decide_preferred_recorder
  4410-4413   delete_archive_entry
  5129-5131   delete_archive_rule
  5904-6051   diag
 25601-25662  einnahmen_cmd
  5071-5074   find_recordings_by_fingerprint
  4431-4447   finish_recording_attempt
  4591-4593   get_all_active_trackings
  4498-4500   get_all_checks
  4938-4941   get_all_recordings
  5020-5022   get_all_tags_with_counts
  5048-5051   get_annotations_for_recording
  4405-4408   get_archive_entry
  5041-5044   get_bookmarked_recordings
  2310-2315   get_cookie_health
  5008-5014   get_event_log
  4454-4468   get_last_recording_attempt
  3455-3497   get_live_status
  5354-5357   get_manual_recordings
  5056-5059   get_or_compute_inspect_sync
  5456-5459   get_outcome_breakdown
  5027-5030   get_priority_poll_interval
  4449-4452   get_recent_recording_attempts
  4943-4946   get_recording_by_id
  5034-5037   get_recording_note
  3868-3897   get_redis
  4527-4530   get_stats
  5409-5413   get_storage_stats
  5149-5151   get_tiktok_status_distribution
  4633-4642   get_tracking_state
  4588-4589   get_trackings_for_group
  5370-5373   get_trash_recordings
 10037-10504  handle_recording_finished
 25711-25716  hilfe_cmd
  4290-4355   init_db
  5121-5123   list_archive_rules
  5689-5727   live
  8552-8582   live_check_worker
  3952-3995   llm_chat
  4018-4049   llm_chat_sync
  4003-4015   llm_list_models
  4967-5000   log_event
  1924-1957   log_recording_failure
  7601-7650   logs_cmd
 27497-27776  main
  6403-6426   on_ai_media
  7727-7753   on_ai_reply
  7808-7837   on_azrael_mention
  7869-7899   on_callback
  9628-9646   on_chat_migration
  7762-7775   on_link_video
 18622-18727  oracle_handle
  7490-7493   pause_tracking
  5469-5474   profile_keyboard
  5642-5686   quelle
  7552-7598   quota
  9025-9099   reaper_loop
  5145-5147   record_tiktok_status
  6442-6472   recstatus
  3899-3907   redis_get_json
  3910-3916   redis_set_json
 25738-25748  report_cmd
 11900-11902  report_proxy_result
  2589-2631   resolve_tiktok_live_stream
  5365-5368   restore_recording
  7496-7499   resume_tracking
  5134-5139   run_archive_rules
 25751-26019  run_bot
 12826-12920  run_flask
  5109-5112   sample_bandwidth_for_active
  4490-4496   save_tiktok_check
  4789-4808   set_recording_file
  4596-4600   set_tracking_paused
  5360-5363   soft_delete_recording
 25696-25708  spenden_cmd
  9652-9663   split_and_send_video
  5552-5594   start
  4415-4429   start_recording_attempt
  6677-6715   stats
  5299-5352   stop_manual_recording
  7502-7549   stoprec
  6901-6909   summary_cmd
  7653-7724   sysres
  6053-6197   teststream
  5596-5637   tiktok
  7318-7375   topusers
  5764-5821   track
  5729-5761   track_exact
  5835-5902   tracklist
  5183-5297   trigger_manual_recording
  4721-4756   try_acquire_recording_lock
  5376-5378   universal_search
 25665-25693  unpause_cmd
  5823-5833   untrack
 25492-25598  update_cmd
  5066-5069   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, class BestandUnbekannt, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, finde_ohne_eintrag, get_archive_entries_paged, get_archive_entry, run_archive_file_check, uebernehmen
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
audiotap.py            diagnose, melden, warum_kein_tap
aufnahmechat.py        ass, ausschnitt, beenden, beginnen, clip_beginnt, clip_fertig, clip_merken, clips_nehmen, clips_offen, concat_liste, einbrennen_cmd, laeuft, modus, notieren, untertitel_cmd, zusammenschnitt_cmd
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelkontext.py       ausfall, block, fakten, letzte_erinnerung, nachricht, restream_quellen, sicher, streamer_waehlen
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungsdienst.py  fuer_deck, grafana_jetzt, grafana_lage, grafana_unit, grund_text, installiert, prometheus_jetzt, prometheus_lage, selbstheilung_erlaubt, steuern
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatnachtrag.py        beilage_lesen, beilage_zu, eingearbeitet, ensure_schema, erledigt, fehlversuch, ist_beilage, lesen, offene, stempel, unveraendert, vormerken
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
clientip.py            echte_ip, host_ist_lokal, ist_https, ist_lokal
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, class KeinDesktop, configure, desktop_pruefen, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, gesetzte, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwartung.py           faellig_in, letzter_lauf, merken, stand_datei
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, mariadb_lage, set_pool, vorrat_groesse, vorrat_lage, vorrat_leeren
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordaufnahme.py     an, beschriftung, hochladen, teilen
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
discordziele.py        clip_kanal, clip_kanal_des_bereichs, clip_kanal_holen, eigene_kanaele, loeschbar, umzugsmarke, umzugsmarke_lesen
donations.py           configure, fmt_eur, kurse_aus_env, parse_number, source_allowed, summe_eur, to_eur, unknown_count, zeile_eur
donationsdb.py         manual_rows, manual_total, parse_eur
durchreicher.py        adresse, ist, main, nutzer_aus, werkzeug, werkzeuge, zieher_cmd, zieher_umgebung, zubringer_cmd
einstellungen.py       bekannt, class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
encodeschlange.py      lage, last_frei, parallel, platz, platz_sync
envdatei.py            class EnvdateiFehler, lesen, main, setzen, wert_lesen, wert_schreiben
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventlog.py            leeren, schreibe, stand
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
fehlertext.py          nach_aussen, saeubern
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      anzeige_groesse, avatar_kette, chat_umbruch_w, chat_zeilen, drawtext_chain, studio_chain, studio_masse
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
forkriegel.py          class Vortritt
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
geschuetzt.py          lage, ruhend, vermerken, verschlossen, zuruecksetzen
heapzaum.py            arenen_wunsch, deckeln, lage, rss_mb, takt_min, zurueckgeben
herkunft.py            entscheiden
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, state_gueltig, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, naechster_cluster, naechster_key, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kickzentrifugo.py      als_frame, antwort_fehler, class KickZentrifugoFehler, connect_cmd, fehler_code, ist_ping, kanal, lage, neue_client_id, neues_token, pause, refresh_cmd, subscribe_cmd, token_aus, ttl_aus, verbindung_body, ws_url_aus, zerlegen, zugang
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_installiert, lokal_stand, lokal_zuerst, lokales_modell, normal, provider
lagebild.py            bauen, dienst_quelle, dienste, dienste_lesen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
linkvideo.py           abklingzeit_s, an, aufraeumen, ausgabe_lesen, befehl, bildunterschrift, configure, darf, grund, holen, ist_tiktok, links, max_dauer_s, sperre, werkzeug
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
livemeldung.py         live_an, live_aus
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           erfolg, gestoert, melden, zuruecksetzen, zusatz
memeklip.py            class Fenster, frage, lies_urteil, soll_clippen
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modki.py               frage, lies_klassifikation, lies_schimpfwoerter
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
overlaybrowser.py      browser_cmd, class Dauerbrowser, class OverlayBrowserFehler
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, runde_gelaufen, uebersicht, vergessen
pruefschlange.py       erledigt, mit_frist, vorgemerkt, vormerken, zuruecksetzen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
raumkennung.py         grund, gueltig
reccmd.py              build_recording_cmd, configure
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
resolvergrund.py       http_grund, quelle_lage, quelle_laut, text
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, ein_start_je_ziel, fenstergroesse, freigeben, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, startend, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, bruecke, bruecke_luecke, bruecke_offline, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamcmd.py         build, configure, drossel_avatar_aus, drossel_bitrate, drossel_canvas, drossel_fps, drossel_preset, drossel_zusatz, fueller, quell_eingang, schriftart, zubringer
restreamgesundheit.py  blind_markieren, frische_tee_fehler, marke_setzen
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              anlegen, create_schema, index_sicher, kollation_angleichen, modultabellen, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        ausnahme_text, class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid, weiche_grund
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
sitzungsschluessel.py  laden, pin_schluessel
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
spendeninfo.py         krypto, paypal, paypal_url, stand, text
spendenziel.py         eingang, fenster_start, ist_monatlich, stand, summe, zeitraum, ziel_eur
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             class BestandUnbekannt, cleanup, forecast, notfall_raeumen, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dashboard_umzug, dauer_text, ersatz, grund, ist_fehler, ist_telegram_chat, migration_plan, migriert_erlaubt, nur_telegram, standardgruppe, text, zuruecksetzen
textmore.py            configure_banned_cap, pre_nachrichten, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             ausfuehrbar_im_archiv, build_plan, check, class Plan, class UpdaterConfig, commit_zip_url, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, rechte_angleichen, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
uploadschlange.py      angekommen, faellig, gleicher, nach_versuch, pause_s
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          bedarf_mb, frei_mb, geladen, name, rss_hinweis, verfuegbar, waehle, wechsel_pruefen
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
zeitglaetter.py        ausdruck, bsf_args, filter_text, verfuegbar
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class GrafanaAgent, class HealthAgent, class LearningAgent, class PrometheusAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime, ohne_denkblock
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler, frische_intervalle
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
