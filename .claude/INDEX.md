# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10168  GET              /                                                dashboard
 12223  GET              /api/abo/status                                  api_abo_status
 12177  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10956  GET              /api/automation/status                           api_automation_status
 10978  POST             /api/automation/toggle                           api_automation_toggle
 19805  GET              /api/channel/categories                          api_channel_categories
 19811  POST             /api/channel/set                                 api_channel_set
 19658  GET              /api/channels/status                             api_channels_status
 19332  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19315  GET              /api/clips                                       api_clips
 19361  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19233  GET              /api/debug/threads                               api_debug_threads
 12188  GET              /api/events                                      api_events
 11667  GET              /api/events/stream                               api_events_stream
 11494  GET              /api/health                                      api_health
 19274  POST             /api/highlights/config                           api_highlights_config
 10102  POST             /api/login                                       dashboard_login_submit
 12513  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11582  GET              /api/notify/status                               api_notify_status
 11593  POST             /api/notify/test                                 api_notify_test
 12277  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12254  GET              /api/proxy/trend                                 api_proxy_trend
 19381  GET              /api/tts/<fn>                                    api_tts_file
 20158  GET              /api/upload_window                               api_upload_window
 11784  GET              /archive/<int:eid>/download                      archive_download
 11812  GET              /download/<int:recording_id>                     download
 11741  GET              /health                                          health
 19142  GET              /healthz                                         healthz
 10093  GET              /login                                           dashboard_login_page
 10123  GET              /logout                                          dashboard_logout
 10130  GET              /manifest.webmanifest                            pwa_manifest
 20131  GET              /overlay                                         overlay_page
 10154  GET              /pwa-icon-<variant>.png                          pwa_icon
 10140  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (343)

```
   195  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   422  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   195  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   165  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   993  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   738  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   864  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   844  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   882  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   806  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   356  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   367  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   377  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   400  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   407  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   418  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   546  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   644  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1231  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1263  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   341  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   946  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   926  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1099  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1147  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1198  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1057  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   901  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   499  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   763  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   645  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   628  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   620  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   456  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   472  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   807  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   374  GET              /api/archive/scan                                api_archive_scan   [nc/routes/archive.py]
   405  POST             /api/archive/scan/adopt                          api_archive_scan_adopt   [nc/routes/archive.py]
   772  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   792  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   679  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    49  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    78  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   163  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    99  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   222  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   120  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   342  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   328  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   350  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   174  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   406  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   397  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   314  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   190  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   231  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   243  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   372  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   281  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   267  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   379  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   342  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   399  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   524  GET              /api/beobachtung/lage                            api_beobachtung_lage   [nc/routes/beobachtung.py]
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
   433  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   418  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   238  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
   195  POST             /api/cookies/fetch                               api_cookies_fetch   [nc/routes/settings.py]
    73  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    80  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   497  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   259  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   286  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   379  POST             /api/db/restore/apply                            api_db_restore_apply   [nc/routes/settings.py]
   323  GET              /api/db/restore/list                             api_db_restore_list   [nc/routes/settings.py]
   341  POST             /api/db/restore/prepare                          api_db_restore_prepare   [nc/routes/settings.py]
   246  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
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
   112  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   120  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    60  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   136  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
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
   200  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   220  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   247  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
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
   222  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   244  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
   103  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   171  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   149  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    85  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   128  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   178  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   267  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   556  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   531  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   308  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   144  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   973  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
  1082  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
  1110  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
  1130  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   960  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
  1022  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
  1009  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   990  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   347  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   635  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   630  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   678  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   561  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   888  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   652  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   615  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   588  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   862  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   732  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   821  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   727  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   660  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   440  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   905  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   528  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   783  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   938  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   923  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   484  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   722  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   708  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   691  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   748  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
  1273  GET              /api/recordings/session/<sid>                    api_recording_session   [nc/routes/recordings.py]
  1394  POST             /api/recordings/session/<sid>/join               api_recording_session_join   [nc/routes/recordings.py]
  1237  GET              /api/recordings/sessions                         api_recording_sessions   [nc/routes/recordings.py]
   841  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   737  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   490  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   468  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   509  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   526  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   578  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   444  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   265  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   165  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   600  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   413  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   134  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   539  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   565  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   191  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   216  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   388  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   474  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   464  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   499  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
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
   544  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   396  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   426  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
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
   239  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   460  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   489  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   409  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   422  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   518  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   395  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   270  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   315  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   339  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   326  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   166  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   284  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   136  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   376  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   431  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
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
   468  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands in discordbot.py (66)

```
  2091  /about                  Ueber diesen Bot
   813  /ai                     
  2091  /aireset                KI-Kontext zuruecksetzen
  1222  /ask                    
   914  /assign_role            
   964  /ban                    
  2046  /botstats               
  2091  /brain                  Brain-Lage: Regeln, Agenten, Empfehlungen
  2091  /bulkadd                Mehrere User auf einmal tracken · a b c
  2091  /cleanup                Alte Aufnahmen aufraeumen
  1477  /clearwarns             
  2010  /clip                   
  1995  /clipoftheweek          
  1348  /clips                  
  2091  /cookies                Cookie-Status — mit 'holen' selbst beziehen · [holen]
   869  /create_category        
   840  /create_channel         
   904  /create_group           
   879  /create_role            
   855  /create_voice           
  1100  /daily                  
  2091  /diag                   Vollstaendige Diagnose
  2091  /einnahmen              Einnahmen und Spenden
  1251  /event                  
  1293  /events                 
  1387  /follow                 
  1376  /help                   
   954  /kick                   
  1075  /leaderboard            
  2091  /live                   Live-Status sofort pruefen · @user
  1335  /livenow                
  2091  /logs                   Letzte Fehler aus dem Log
  2091  /pause                  Tracking pausieren · @user
  1363  /post_test              
  1183  /profile                
   986  /purge                  
  2091  /quelle                 Stream-Quellen eines Live-Nutzers messen (alle Wege, ffprobe
  2091  /quota                  Speicher-Quota
  1062  /rank                   
  1323  /recstatus              
   924  /remove_role            
  2091  /report                 Azrael-Sentinel-Wochenreport
   826  /restream_status        
  2091  /resume                 Tracking fortsetzen · @user
   934  /set_channel_perms      
  1029  /setup_community        
  1046  /setup_targets          
  1419  /stats                  
   785  /status                 
  2091  /stoprec                Laufende Aufnahme sauber beenden · @user
  1515  /streaminfo             
  2091  /summary                Tageszusammenfassung
  2091  /sysres                 System-Ressourcen
  2091  /teststream             Recorder-Selbsttest · @user
  2091  /tiktok                 Profil-Analyse eines TikTok-Accounts · ‹name›
   974  /timeout                
  1487  /topstreamers           
  2091  /topusers               Top-Streamer nach Aufnahmen
   715  /track                  
  2091  /track_exact            Exakten Usernamen tracken (ohne Korrektur) · ‹name›
   798  /tracklist              
  1401  /unfollow               
  2091  /unpause                Auto-pausierte Quelle wieder aktivieren · @user
   747  /untrack                
  1440  /warn                   
  1463  /warnings               
```

## Discord-Events in discordbot.py (4)

```
  2249  on_member_join
  2211  on_message
  2112  on_raw_reaction_add
  2284  on_ready
```

## Top-Level-Symbole in telegramversand.py (2 Funktionen)

```
    58-73     konfiguriere
    76-476    split_and_send_video
```

## Top-Level-Symbole in discordbot.py (46 Funktionen)

```
  1592-1643   _award_xp
  1814-1843   _clip_week_leader
  1867-1881   _clipoftheweek_loop
  2400-2462   _community_events_loop
  1549-1571   _dc_client
  1574-1583   _dc_offen
  2502-2537   _disc_automod_check
   403-408    _disc_sprache_setzen
  1646-1694   _discord_ai_automod
   536-575    _discord_automod
  1697-1717   _discord_azrael_reply
  1884-2359   _discord_run_once
   238-296    _discord_start
   299-353    _ensure_discord_invite
  2365-2397   _ensure_error_channel
   424-437    _ensure_rank_roles
   678-692    _ensure_team_roles
  2465-2495   _error_channel_loop
   585-589    _guard
   505-533    _handle_voice_ai
   411-421    _is_admin
  1762-1773   _liveboard_loop
   592-610    _on_level_up
   501-502    _par_chat_id
  1846-1864   _post_clip_of_week
  1776-1794   _post_weekly_digest
   440-466    _provision_base_channels
   469-485    _provision_user_channels
  1315-1408   _reg_betrieb
  1000-1089   _reg_community_setup
  1092-1172   _reg_daily_profil
  1215-1312   _reg_frage_events
   772-828    _reg_info
   946-997    _reg_moderation
  1175-1212   _reg_profil
   895-943    _reg_rollen
   831-892    _reg_server
  1411-1498   _reg_streamer
  1501-1546   _reg_system
   706-769    _reg_tracking
   645-675    _run_tg_handler
   488-498    _tracked_usernames
   155-217    _uebernehmen
  1726-1759   _update_liveboard
  1797-1811   _weekly_digest_loop
   220-223    starte
```

## Top-Level-Symbole in bot.py (541 Funktionen, 2 Klassen)

```
 25014-25036  _abbruch_datenbank_unlesbar
  2661-2662   _abo_key
  2682-2700   _abo_probe_dump
 25132-25148  _abschied_wachen
 25151-25169  _abschluss
 16031-16038  _ad_allowlist
 17030-17036  _agent_for
 17039-17055  _ai_telemetry
 17552-17570  _alert
 21026-21076  _alert_monitor_loop
 21458-21520  _announce_loop
  3547-3557   _anthropic_key
  3564-3566   _anthropic_model
  9785-9788   _arg_int
  2653-2658   _as_dict
 24758-24767  _async_exc_handler
 17733-17755  _audio_tap_cmd
 18313-18372  _audio_tap_melden
 17769-17793  _audio_tap_sammler
  9134-9167   _aufnahme_beim_stopp_sichern
 24007-24009  _aufnahme_deckel
  9170-9188   _aufnahme_platz_frei
 25096-25116  _aufnahmen_abschliessen
 25039-25093  _aufraeumen
  9956-10025  _auth_cookie
  9923-9952   _auth_guard
  1903-1908   _auto_on
 18999-19017  _auto_restream_loop
 13725-13767  _avatar_frames_laden
 22541-22556  _azrael_broadcast_reply
 22441-22463  _azrael_chat_reply
 22413-22438  _azrael_chat_should_reply
 22469-22471  _azrael_gate_cfg
 17060-17074  _azrael_live_state
 20044-20058  _azrael_overlay_state
 17434-17488  _azrael_proactive_loop
 16878-16934  _azrael_reaction_to_chats
 22474-22481  _azrael_reply_all_chats
 22400-22410  _azrael_self_names
 22509-22538  _azrael_send_to
 13686-13722  _azrael_spricht
 14029-14042  _azrael_stimme_stumm
 17080-17101  _azrael_system
 21160-21163  _backup_active
 21241-21254  _backup_loop
 24096-24100  _betrieb
 24831-24840  _brain_crowdsec_snap
 24941-24944  _brain_db_health
 20947-20956  _brain_growth_loop
 10347-10374  _brain_growth_snapshot
  2586-2606   _brain_hint_delay
 24903-24938  _brain_moderation_snap
  6489-6517   _brain_notify
 24947-24969  _brain_recording_snap
 24843-24900  _brain_restream_health
 24972-24985  _brain_tiktok_status_snap
 11646-11663  _browser_push
  6529-6616   _build_daily_summary
 14076-14080  _build_restream_cmd
  5242-5269   _can_stop_tracking
  2016-2038   _capture_set_cookies
 12331-12334  _cfg_get
 12337-12339  _cfg_set
 19766-19801  _channel_set_all
 12914-12917  _chat_connected
 12920-12936  _chat_disconnected
  8777-8788   _chat_is_forum
 18120-18145  _chat_listener_abbauen
 12956-12958  _chat_sanitize
 12899-12911  _chat_stat
 12939-12942  _chat_stats_snapshot
  3865-3877   _check_ai_models_sync
 10629-10672  _classify_pool_anonymity
 10675-10692  _classify_pool_anonymity_bg
   894-916    _claude_chat_sync_metered
  9817-9824   _client_ip
 21604-21631  _clip_prune
 21634-21644  _clip_recfile_for
 22057-22063  _clip_should_velocity
 21686-21768  _clip_to_discord
  3751-3760   _close_ai_session
 22587-22602  _cohost_broadcast
 22572-22573  _cohost_cfg
 22628-22640  _cohost_fire_highlight
 22576-22584  _cohost_gate
 22605-22625  _cohost_highlight
 10277-10279  _conv_messages
  6888-6949   _cookie_alarm_loop
  2106-2107   _cookie_autofetch_info
  2090-2094   _cookie_autorefresh_info
 24465-24487  _cookie_bezug_loop
 24490-24515  _cookie_bezug_runde
  1993-1997   _cookie_header
  2119-2133   _cookies_selbst_holen
  4081-4083   _create_index_safe
 20490-20604  _crowdsec_status
 20436-20487  _crowdsec_via_lapi
 20340-20358  _cscli_bin
 20367-20380  _cscli_path
  6778-6803   _daily_summary_loop
 20398-20415  _darf_journal_lesen
  3076-3101   _darf_ytdlp_nachschlagen
 11827-11848  _dashboard_adresse
 21000-21023  _db_maintenance_loop
  6747-6775   _db_vacuum_loop
 16054-16078  _detect_foreign_ad
  1583-1594   _diag_path_owner
 17339-17384  _director_finalize
 18302-18309  _director_for
 17288-17336  _director_mark
 21920-21923  _disc_state_get
 21926-21933  _disc_state_set
 20928-20937  _discord_bot_starten
 20891-20902  _discord_einladung_merken
 20940-20944  _discord_invite
 20905-20925  _discord_kontext
 21881-21917  _discord_live_thread
 17491-17503  _discord_notify
 20863-20888  _discord_ops_alert
 21779-21877  _discord_post_user
 21523-21529  _discord_stop
  6806-6883   _disk_alarm_loop
 24390-24439  _disk_autoclean
 24613-24626  _disk_guard_loop
 13664-13671  _drossel_hoeher
 13660-13661  _drossel_stufe
 13674-13682  _drossel_zuruecksetzen
 12004-12006  _dump_all_threads
 24103-24117  _einstellungen_startzeile
 10555-10618  _enrich_proxies_with_geo
  2162-2223   _ensure_cookie_file_netscape
  8836-8839   _ensure_notify_topic
 10799-10836  _ensure_proxy_ready
  8790-8817   _ensure_topic
   737-739    _env_int
   742-744    _env_int_range
 17536-17549  _event_webhook
 12682-12695  _evolution_loop
  5931-5965   _extract_file_payload
  2295-2297   _extract_urls_from_streamurl_node
 20383-20390  _f2b_sudo_hint
 25172-25235  _fatal_vom_botteil
 24012-24027  _fd_grenze_anheben
  4706-4716   _fehler_text
 10456-10474  _fetch_proxy_list
 18089-18117  _fetch_tiktok_room_id
   820-823    _ff_cmd
 13493-13498  _find_chromium
  3467-3469   _find_external_recorder
  2300-2302   _find_stream_urls
 12382-12407  _fire_webhooks
  7715-7724   _fork_safe
   927-940    _freeai_chat_sync_metered
 20429-20433  _geo_lookup_ips
  3739-3748   _get_ai_session
  7548-7588   _get_live_info
  2927-2934   _get_resolve_semaphore
  8040-8430   _handle_single_tracking
 24212-24214  _hb
 24217-24234  _hb_while
 12970-12972  _highlight_cfg
 12975-13004  _highlight_observe
 13501-13519  _htmlov_screenshot_cmd
 17795-17805  _httpx_proxy
 12415-12427  _in_quiet_hours
 25000-25011  _init_db_oder_abbruch
 25819-25850  _install_fast_eventloop
  9680-9734   _install_fast_json
 12009-12025  _install_faulthandler
 19045-19054  _intel_ensure_schema
 19097-19132  _intel_index_loop
 19066-19081  _intel_index_one
 19057-19063  _intel_semantic
  5231-5240   _is_authorized
  7926-7947   _is_dead
  2285-2287   _is_hevc
 20418-20420  _is_private_ip
  1802-1809   _is_process_running
  6519-6526   _is_quiet_hours
  1376-1385   _is_upload_window
  4571-4586   _iso
  9769-9782   _json_error_handler
  6741-6742   _kick_broadcaster_id
  6653-6695   _kick_follower_count
  6637-6640   _kick_slug
 11459-11466  _kick_user_token
  7847-7872   _kick_ws_pause
 24988-24997  _kickmod_boot
  4161-4164   _kind_from_filename
 12444-12446  _latest_popularity
  1739-1748   _laufstand
 24573-24610  _laufstand_loop
 24136-24174  _leistung_erheben
 18708-18757  _live_react_loop
 18375-18697  _live_react_worker
  3317-3429   _live_status_aufloesen
 16937-16948  _live_transcript_push
 18699-18706  _live_users
 17387-17431  _living_title_loop
 21166-21238  _local_backup_scan
  9751-9765   _log_5xx
 24177-24209  _log_schleuse_pruefen
   810-817    _log_sicher
 14088-14100  _looks_like_codec_err
 14083-14085  _looks_like_source_expired
  7765-7795   _loop_fehler
 12029-12038  _loop_heartbeat
 23918-23951  _loop_lag_monitor
 23965-23985  _loop_stockung_melden
 23988-23998  _loop_takt_starten
 12041-12114  _loop_watchdog_thread
 16814-16831  _loyalty_add
 16805-16811  _loyalty_get
 16834-16842  _loyalty_top
 12554-12556  _manual_donations_total
  4913-4932   _manual_status
  7949-7950   _mark_dead
 11075-11091  _marketing_loop
 22488-22506  _maybe_handle_command
 24712-24736  _maybe_hype_clip
 21573-21601  _meme_klassifizieren
  4068-4073   _migrate_columns
 22767-22778  _mod_is_exempt
 22781-22786  _mod_warn_first
 22789-22792  _mod_warn_text
 12739-12758  _modlog
 12722-12736  _modlog_schreiben
  1072-1074   _multistream_targets
  3104-3140   _nachschlag_ytdlp
  7727-7728   _nc_create_subprocess_exec
  7731-7732   _nc_create_subprocess_shell
 11396-11413  _news_loop
 12781-12783  _normalize_ingest
  2517-2534   _note_check_duration
  8830-8833   _notify_topic_name
  3143-3163   _ohne_url_melden
 16963-16971  _oracle_memories
 17237-17271  _oracle_memorize
 16974-16987  _oracle_persona
 16956-16960  _oracle_recent_text
 13127-13128  _ov_atomic_write
 13118-13120  _ov_bar
 15957-15969  _ov_clip_text
 13123-13124  _ov_oneline
 20095-20124  _overlay_push
 13447-13490  _overlay_render_size
 12850-12854  _overlay_session_reset
 20060-20062  _overlay_src_ok
 16041-16051  _own_invites
 13442-13444  _parse_size
 20612-20692  _parse_ssh_attacks
  7150-7183   _pause_resume_cmd
  2044-2088   _persist_refreshed_cookies
  1947-1979   _pick_checked_pull_proxy
  9853-9866   _pin_auth_value
  9912-9913   _pin_clear_fail
  9892-9895   _pin_locked
  9898-9909   _pin_note_fail
  9869-9889   _pin_ok
 19902-19927  _piper_pick_model
 19987-20038  _piper_say
 12344-12379  _post_json_threaded
 13421-13439  _probe_video_size
  1830-1847   _proc_is_recorder
 10768-10796  _proxy_pool_refresh_loop
  1913-1944   _proxy_report_recording
  8528-8566   _pruefstand_melden
 24047-24058  _pruefung_verworfen
 11994-11996  _prune_stall_dumps
 11145-11315  _public_stats
  2110-2116   _pull_proxy_still
 17507-17533  _push_notify
 10072-10074  _pwa_dir
 10525-10540  _quick_validate_proxy
 12410-12412  _quiet_hours_config
 10037-10070  _rate_guard
 16775-16781  _react_warn
  7635-7674   _reap_proc
  9064-9131   _rec_auto_abschalten
  9011-9061   _rec_frueh_getrennt
  8894-8956   _rec_kategorie_melden
  8959-9008   _rec_totstreak_fortschreiben
  2557-2579   _record_check_outcome
   805-807    _redact_stream_urls
 10695-10765  _refresh_proxy_pool
  2334-2425   _resolve_via_html
  2707-2904   _resolve_via_webcast_api_v2
  2967-3052   _resolve_via_ytdlp
 22097-22226  _resolve_youtube_ingest
  2311-2331   _resolver_stumm
 12833-12844  _restream_active_sources
 13770-13894  _restream_avatar_feeder_start
 13897-13906  _restream_avatar_feeder_stop
 18148-18266  _restream_chat_guardian
 13007-13079  _restream_chat_push
 13104-13113  _restream_chat_push_async
 13522-13631  _restream_html_overlay_start
 13634-13647  _restream_html_overlay_stop
 12792-12815  _restream_overlay_files
 18761-18793  _restream_platform_state
 18961-18996  _restream_resume_after_restart
 13954-14026  _restream_tts_enqueue_wav
 13383-13415  _restream_tts_feeder
 13380-13381  _restream_tts_fifo_path
 13909-13936  _restream_tts_start
 13938-13952  _restream_tts_stop
 18799-18958  _restream_verify_loop
 21131-21143  _retention_loop
 21125-21128  _retention_scan
  2664-2666   _room_is_abo
  5969-6086   _run_ai_call
 12137-12150  _run_async_from_flask
 20423-20426  _run_priv
 25807-25815  _run_selfcheck_and_exit
 21146-21157  _s3_client
  7976-8027   _safe_send
  4839-4855   _sample_net_throughput
  2609-2639   _schedule_next_check
 21079-21122  _scheduler_loop
  4076-4078   _schema_pk
 12154-12159  _scraper_session
 22795-22834  _screen_full
 11510-11547  _sec_headers
  2290-2292   _select_stream_from_data_section
 25527-25804  _selfcheck
  8842-8876   _send_live_notice
  1399-1403   _should_defer_upload
 21647-21683  _shrink_for_discord
 10077-10089  _sicheres_ziel
 20959-20997  _sicherheits_erinnerung_loop
 24633-24650  _sign_health_check
 24653-24672  _sign_health_loop
  4589-4614   _sitzung_bestimmen
  7744-7755   _spawn
 26232-26262  _spawn_from_flask
 24061-24067  _speicher_maps
 24070-24085  _speicher_pflegen
 17807-18086  _start_chat_listener
 24030-24044  _start_gesperrt
 12117-12134  _start_loop_watchdog
 11342-11391  _stats_loop
 11321-11324  _stats_output_path
 11327-11339  _stats_write
 19939-19953  _stimme_saubern
 19960-19984  _stimme_schon_gesagt
  8509-8525   _storage_cleanup_loop
 24692-24699  _story_for
  3492-3498   _stream_url_expiry
  3500-3505   _stream_url_ttl
 16004-16011  _streamer_persona_get
 21263-21415  _system_backup
 21424-21454  _system_backup_loop
 11954-11972  _task_auf_bot_schleife
 23608-23624  _telegram_befehlsmenue
  7798-7844   _telegram_polling_fehler
 10477-10516  _test_proxy
 11023-11039  _testpush_resolve_live
  7952-7973   _tg_sprache_setzen
  8749-8759   _tg_topics_load_into_mem
  8746-8747   _tg_topics_path
  8761-8768   _tg_topics_save
  9827-9835   _token_ok
  8771-8775   _topic_forget
 12430-12441  _tracking_max_duration
  4369-4383   _tracking_remove_cleanup
  4400-4412   _tracking_resume_cleanup
  1641-1664   _try_attach_file_handler
 19929-19937  _tts_cleanup
 10999-11003  _tunnel_effective
 24442-24462  _tunnel_lage
 24518-24570  _tunnel_wacht_loop
 19425-19478  _twitch_channel_status
 22837-22982  _twitch_chat_loop
 21939-21952  _twitch_clip_versuchen
 22651-22754  _twitch_eventsub_loop
  1422-1435   _upload_queue_add
  1446-1448   _upload_queue_count
  1405-1414   _upload_queue_load
  1395-1397   _upload_queue_path
  1437-1444   _upload_queue_remove
  1416-1420   _upload_queue_save
  1450-1491   _upload_window_loop
  7608-7615   _uptime_s
 12769-12778  _url_host
  3166-3265   _url_nachschlag
   887-891    _usage_record_claude
 24806-24828  _v37_pause_source
 24770-24780  _v37_restream_restart
 24783-24803  _v37_unpause_source
  7875-7919   _verbindung_verloren
  6698-6729   _viewer_sample_loop
  9916-9919   _wants_html
  7618-7632   _warn_empty_env
 24255-24376  _watchdog_loop
 22372-22380  _wchat_thank_ok
 17575-17605  _whisper_get_model
  7705-7712   _whisper_native_section
 16762-16768  _whisper_pool
 17699-17731  _whisper_segments
 17607-17623  _whisper_stumm
 17626-17696  _whisper_transcribe
 13175-13337  _write_restream_overlay
 13137-13172  _write_restream_overlay_async
 23006-23102  _youtube_api_chat_loop
 19481-19584  _youtube_api_status
 19587-19654  _youtube_channel_status
 23105-23266  _youtube_chat_loop
 21955-21980  _youtube_clip_versuchen
 22232-22245  _youtube_restream_autoconfig
 22248-22272  _youtube_restream_autoconfig_inner
 22339-22367  _youtube_send
 19722-19763  _youtube_set_channel
 22275-22309  _yt_access_token
 22312-22327  _yt_live_chat_id
 22335-22336  _yt_sendrate_cfg
 22985-23000  _yt_timeout
  2951-2952   _ytdlp_detect_available
  2954-2965   _ytdlp_note_result
 11999-12001  _zombie_child_count
 24120-24133  _zustand_kennzahlen
  7484-7508   about
  4280-4284   add_ai_log_entry
  4197-4200   add_archive_entry
  4877-4879   add_archive_rule
  4617-4688   add_recording
  4344-4361   add_tracking
  6089-6122   ai
  3891-3972   ai_chat
  4006-4016   ai_history_append
  4018-4023   ai_history_clear
  3995-4004   ai_history_load
  3980-3993   ai_rate_limit_check
  6151-6159   aireset
 17104-17123  azrael_chat
 23271-23393  brain_cmd
  3508-3513   build_recording_cmd
  4364-4367   bulk_add_trackings
  6952-7011   bulkadd
  8569-8729   check_all_trackings
  4416-4428   claim_live_transition
 16081-16694  class KickModerator
 14103-15844  class RestreamManager
 10882-10924  classify_proxy_anonymity
  6197-6395   cleanup
  5167-5173   cleanup_old_recordings
  4562-4569   clear_recording
 21983-22054  clip_moment
  4829-4832   compute_storage_forecast
  7074-7147   cookies_cmd
  4335-4341   count_trackings_for_chat
  4267-4278   decide_preferred_recorder
  4207-4210   delete_archive_entry
  4881-4883   delete_archive_rule
  5626-5773   diag
 23505-23566  einnahmen_cmd
  4823-4826   find_recordings_by_fingerprint
  4228-4244   finish_recording_attempt
  4388-4390   get_all_active_trackings
  4295-4297   get_all_checks
  4690-4693   get_all_recordings
  4772-4774   get_all_tags_with_counts
  4800-4803   get_annotations_for_recording
  4202-4205   get_archive_entry
  4793-4796   get_bookmarked_recordings
  2150-2155   get_cookie_health
  4760-4766   get_event_log
  4251-4265   get_last_recording_attempt
  3268-3310   get_live_status
  5106-5109   get_manual_recordings
  4808-4811   get_or_compute_inspect_sync
  5208-5211   get_outcome_breakdown
  4779-4782   get_priority_poll_interval
  4246-4249   get_recent_recording_attempts
  4695-4698   get_recording_by_id
  4786-4789   get_recording_note
  3679-3708   get_redis
  4324-4327   get_stats
  5161-5165   get_storage_stats
  4901-4903   get_tiktok_status_distribution
  4430-4439   get_tracking_state
  4385-4386   get_trackings_for_group
  5122-5125   get_trash_recordings
  9191-9659   handle_recording_finished
 23600-23605  hilfe_cmd
  4091-4152   init_db
  4873-4875   list_archive_rules
  5411-5449   live
  8030-8038   live_check_worker
  3763-3802   llm_chat
  3825-3855   llm_chat_sync
  3810-3822   llm_list_models
  4719-4752   log_event
  1764-1797   log_recording_failure
  7297-7346   logs_cmd
 25238-25517  main
  6125-6148   on_ai_media
  7423-7449   on_ai_reply
  7452-7481   on_azrael_mention
  7513-7543   on_callback
 17129-17234  oracle_handle
  7186-7189   pause_tracking
  5221-5226   profile_keyboard
  5364-5408   quelle
  7248-7294   quota
  8432-8506   reaper_loop
  4897-4899   record_tiktok_status
  6164-6194   recstatus
  3710-3718   redis_get_json
  3721-3727   redis_set_json
 23627-23637  report_cmd
 10927-10929  report_proxy_result
  2428-2470   resolve_tiktok_live_stream
  5117-5120   restore_recording
  7192-7195   resume_tracking
  4886-4891   run_archive_rules
 23640-23898  run_bot
 11851-11945  run_flask
  4861-4864   sample_bandwidth_for_active
  4287-4293   save_tiktok_check
  4554-4560   set_recording_file
  4393-4397   set_tracking_paused
  5112-5115   soft_delete_recording
  8882-8892   split_and_send_video
  5274-5316   start
  4212-4226   start_recording_attempt
  6398-6436   stats
  5051-5104   stop_manual_recording
  7198-7245   stoprec
  6622-6630   summary_cmd
  7349-7420   sysres
  5775-5919   teststream
  5318-5359   tiktok
  7014-7071   topusers
  5486-5543   track
  5451-5483   track_exact
  5557-5624   tracklist
  4935-5049   trigger_manual_recording
  4515-4552   try_acquire_recording_lock
  5128-5130   universal_search
 23569-23597  unpause_cmd
  5545-5555   untrack
 23396-23502  update_cmd
  4818-4821   update_recording_fingerprint
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
aufnahmefolge.py       aufnahme_geglueckt, daten_geflossen, melden_erlaubt, nach_403, nach_frueher_trennung, nach_totem_versuch, sitzung_zuende, sperre_rest, stall_grenze
aufnahmekategorie.py   kategorisiere
aufnahmesitzung.py     abdeckung, angleich_cmd, braucht_angleich, concat_cmd, concat_liste, gehoert_dazu, luecken, probe_cmd, sekunden, sitzung_id, tonformat, zieldatei
auslieferung.py        schreibe, stand, text
avatarloop.py          blinzeln, ruhe_seit, schleife, zustand
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
befehle.py             beschreibung, discord_nativ, discord_ueber_tg, fuer, hilfe_text, pruefen, telegram_handler
beobachtungslage.py    grafana, lage, prometheus
betriebslage.py        abschiedswache, bereit, bewerten, haengende_threads, sichern_beim_stopp
binresolve.py          resolve
botctx.py              class BotKontext
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatfolge.py           entscheide
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           anzeigename, configure, darf_pingen, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, rollen_id, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookiebezug.py         anstossen, configure, faellig, gast_hilft, holen, info, intervall_s, naechster_lauf
cookieholen.py         aktualisiere, aus_browser, configure, hole_gastcookies, schreibe, zusammenfuehren
cookies.py             configure, gesundheit, lade_jar, load_dict
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, erwartete_namen, fehlende_namen, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dashauth.py            erlaubt_offen, geschuetzt, host, lage, nur_lokal, offen_im_netz, zurueckgefallen
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbgesundheit.py        messen
dbrestore.py           archive, dump_aus_archiv, einsetzen, einspielen, vorbereiten
dbwrap.py              class DatenbankUnlesbar, configure_db, datei_diagnose, db_async, db_conn, get_pool, set_pool
ddlsafe.py             ddl, ist_schon_da
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
director.py            class LiveDirector, configure
discordlimits.py       aktuell_label, aktuell_mb, configure, describe, effective_upload_mb, gate_mb, guild_filesize_bytes, guild_limit_mb
discordrang.py         rang_fuer_level, slug, xp_fuer_level, xp_zu_level
discordstate.py        invite, state_get
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
einstellungen.py       class Abgelehnt, db_werte, geheim, gueltiger_name, in_umgebung_laden, katalog, pruefen, schutzgrund, setzen, startbericht, uebernehmen, uebersicht, zuruecksetzen
envdatei.py            class EnvdateiFehler, lesen, main, setzen
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
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, dienstmeldung, katalog_kennt, last_errors, list_models_sync, stream_haeppchen, stream_rest
gegendruck.py          abgewiesen, deckel_auto, fd_grenze_anheben, fd_lage, freigeben, lage, reservieren, reserviert, start_entscheiden, verworfen, zuruecksetzen
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kennzahlen.py          einwertig, prometheus, prozess, stand, veroeffentlichen, zeile
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             app_token, broadcaster_id, channel_info, class PusherGeschlossen, configure, oauth_exchange, pusher_fehler, pusher_lage, pusher_pause, pusher_url, schliessgrund, search_category, send_message, slug, timeout_user, update_channel, user_token
kindprozess.py         alle_beenden, ausfuehren, beenden, lage, zuruecksetzen
kiwahl.py              backend, lokal_stand, lokal_zuerst, normal, provider
lagebild.py            bauen, restream_lage
lastvorsorge.py        freie_kerne, jung, startstufe
laufstand.py           befehl, veraltet, vergleich
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
livecache.py           aufraeumen, aufraeumen_faellig, dauer, einflug, frisch, holen, setzen, statistik, zaehle, zaehler_zuruecksetzen
livefolge.py           beste_url, braucht_url_nachschlag, hat_stream_url, last_dehnung, live_gesehen, offline_bestaetigt, poll_abstand, ruhezeit
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             fuer_log, redact_cookie_zeilen, redact_pull_urls, redact_stream_urls, url_ohne_zugang
logschleuse.py         class Schleuse, einreihen, entkoppeln, nachziehen, schwaerzen, stoppen, synchrone_handler, verloren, wartend, zuruecksetzen
looplag.py             bremser, erfassen, lage, spaeher_starten, stelle_aus_rahmen, takt, zuruecksetzen
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
mariadbumzug.py        class UmzugAbgebrochen, env_setzen, geoeffnet_von, in_benutzung, quelle_zaehlen, umziehen, vergleichen, ziel_zaehlen
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
meldetakt.py           melden, zuruecksetzen, zusatz
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
overlaytext.py         configure, latest_popularity, ov_atomic_write, ov_bar, ov_oneline, overlay_src_ok
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
profildetail.py        datum, felder, kennzahlen, kontotyp, verlauf
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
prueflage.py           fuer_healthz, lage, merken, uebersicht, vergessen
qrsvg.py               qr_svg
quellprobe.py          empfehlung, form, kurz, main, maske, messen, probe_durchreicher, probe_ffprobe, probe_html, probe_ytdlp, ttl
quellstat.py           lage, zaehlen, zuruecksetzen
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
schema.py              anlegen, create_schema, index_sicher, parameter, spalten_nachziehen
schemastand.py         lege_an, lies, pruefe, schreibe, streng
schnappschuss.py       class Schnappschuss
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendebruecke.py        class Bruecke, class TsUmschreiber, ist_keyframe, pat_pmt_pid, pes_zeit, pid, pmt_stroeme, pmt_urteil, video_pid
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sicherpfad.py          pruefe_unter, sicher_join, sicherer_name, unter
sicherungspruefung.py  archiv_lesbar, dump_vollstaendig, pruefen
speicherpflege.py      abgelaufene_weg, alte_stempel_weg, groessen
sqldialekt.py          bei_konflikt
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
systemprobe.py         active_recorder, ai_alive, ai_calls_total, cache_leeren, cached_probe, configure, cpu_load_snapshot, disk_pct, recorder_pref, recordings_dir, redis_alive, redis_url, redis_version
telegramfehler.py      dauer_text, grund, ist_fehler, ist_telegram_chat, text, zuruecksetzen
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tgmarkdown.py          html_zu_md, teilen
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
tonspur.py             class Fehlschlag, garantie, garantie_cmd, hat_ton, hat_tonspur, ist_tonlos_fehler, nachruest_cmd, pruef_cmd, pruefen, sichern, stille_eingabe
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
tunnelwacht.py         lage, meldung, probe, probe_cmd
twitchoauth.py         access_token, authorize_url, configure, create_clip, exchange_code, forget, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             build_stamp, changelog, current, latest, summary_line
videoteil.py           configure, dauer, ist_kaputter_container, kopier_teilen, neu_kodieren, platz_reicht, reparieren, wegwerfen, zeitstempel_richten, zu_gross
webserver.py           bindung, ist_loopback, schema, threads, tls_lage, waehle
whispercfg.py          geladen, name, verfuegbar, waehle
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytdlpurl.py            nur_frische, urls_aus_json
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status, upload_clip
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DatabaseAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
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
