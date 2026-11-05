# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (34)

```
 10156  GET              /                                                dashboard
 12211  GET              /api/abo/status                                  api_abo_status
 12165  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10944  GET              /api/automation/status                           api_automation_status
 10966  POST             /api/automation/toggle                           api_automation_toggle
 19793  GET              /api/channel/categories                          api_channel_categories
 19799  POST             /api/channel/set                                 api_channel_set
 19646  GET              /api/channels/status                             api_channels_status
 19320  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 19303  GET              /api/clips                                       api_clips
 19349  POST/DELETE      /api/clips/clear                                 api_clips_clear
 19221  GET              /api/debug/threads                               api_debug_threads
 12176  GET              /api/events                                      api_events
 11655  GET              /api/events/stream                               api_events_stream
 11482  GET              /api/health                                      api_health
 19262  POST             /api/highlights/config                           api_highlights_config
 10090  POST             /api/login                                       dashboard_login_submit
 12501  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11570  GET              /api/notify/status                               api_notify_status
 11581  POST             /api/notify/test                                 api_notify_test
 12265  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12242  GET              /api/proxy/trend                                 api_proxy_trend
 19369  GET              /api/tts/<fn>                                    api_tts_file
 20146  GET              /api/upload_window                               api_upload_window
 11772  GET              /archive/<int:eid>/download                      archive_download
 11800  GET              /download/<int:recording_id>                     download
 11729  GET              /health                                          health
 19130  GET              /healthz                                         healthz
 10081  GET              /login                                           dashboard_login_page
 10111  GET              /logout                                          dashboard_logout
 10118  GET              /manifest.webmanifest                            pwa_manifest
 20119  GET              /overlay                                         overlay_page
 10142  GET              /pwa-icon-<variant>.png                          pwa_icon
 10128  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (339)

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

## Top-Level-Symbole in bot.py (539 Funktionen, 2 Klassen)

```
 24978-25000  _abbruch_datenbank_unlesbar
  2649-2650   _abo_key
  2670-2688   _abo_probe_dump
 25096-25112  _abschied_wachen
 25115-25133  _abschluss
 16019-16026  _ad_allowlist
 17018-17024  _agent_for
 17027-17043  _ai_telemetry
 17540-17558  _alert
 21014-21064  _alert_monitor_loop
 21446-21508  _announce_loop
  3535-3545   _anthropic_key
  3552-3554   _anthropic_model
  9773-9776   _arg_int
  2641-2646   _as_dict
 24728-24737  _async_exc_handler
 17721-17743  _audio_tap_cmd
 18301-18360  _audio_tap_melden
 17757-17781  _audio_tap_sammler
  9122-9155   _aufnahme_beim_stopp_sichern
 23994-23996  _aufnahme_deckel
  9158-9176   _aufnahme_platz_frei
 25060-25080  _aufnahmen_abschliessen
 25003-25057  _aufraeumen
  9944-10013  _auth_cookie
  9911-9940   _auth_guard
  1891-1896   _auto_on
 18987-19005  _auto_restream_loop
 13713-13755  _avatar_frames_laden
 22529-22544  _azrael_broadcast_reply
 22429-22451  _azrael_chat_reply
 22401-22426  _azrael_chat_should_reply
 22457-22459  _azrael_gate_cfg
 17048-17062  _azrael_live_state
 20032-20046  _azrael_overlay_state
 17422-17476  _azrael_proactive_loop
 16866-16922  _azrael_reaction_to_chats
 22462-22469  _azrael_reply_all_chats
 22388-22398  _azrael_self_names
 22497-22526  _azrael_send_to
 13674-13710  _azrael_spricht
 14017-14030  _azrael_stimme_stumm
 17068-17089  _azrael_system
 21148-21151  _backup_active
 21229-21242  _backup_loop
 24083-24087  _betrieb
 24801-24810  _brain_crowdsec_snap
 20935-20944  _brain_growth_loop
 10335-10362  _brain_growth_snapshot
  2574-2594   _brain_hint_delay
 24873-24908  _brain_moderation_snap
  6477-6505   _brain_notify
 24911-24933  _brain_recording_snap
 24813-24870  _brain_restream_health
 24936-24949  _brain_tiktok_status_snap
 11634-11651  _browser_push
  6517-6604   _build_daily_summary
 14064-14068  _build_restream_cmd
  5230-5257   _can_stop_tracking
  2004-2026   _capture_set_cookies
 12319-12322  _cfg_get
 12325-12327  _cfg_set
 19754-19789  _channel_set_all
 12902-12905  _chat_connected
 12908-12924  _chat_disconnected
  8765-8776   _chat_is_forum
 18108-18133  _chat_listener_abbauen
 12944-12946  _chat_sanitize
 12887-12899  _chat_stat
 12927-12930  _chat_stats_snapshot
  3853-3865   _check_ai_models_sync
 10617-10660  _classify_pool_anonymity
 10663-10680  _classify_pool_anonymity_bg
   882-904    _claude_chat_sync_metered
  9805-9812   _client_ip
 21592-21619  _clip_prune
 21622-21632  _clip_recfile_for
 22045-22051  _clip_should_velocity
 21674-21756  _clip_to_discord
  3739-3748   _close_ai_session
 22575-22590  _cohost_broadcast
 22560-22561  _cohost_cfg
 22616-22628  _cohost_fire_highlight
 22564-22572  _cohost_gate
 22593-22613  _cohost_highlight
 10265-10267  _conv_messages
  6876-6937   _cookie_alarm_loop
  2094-2095   _cookie_autofetch_info
  2078-2082   _cookie_autorefresh_info
 24435-24457  _cookie_bezug_loop
 24460-24485  _cookie_bezug_runde
  1981-1985   _cookie_header
  2107-2121   _cookies_selbst_holen
  4069-4071   _create_index_safe
 20478-20592  _crowdsec_status
 20424-20475  _crowdsec_via_lapi
 20328-20346  _cscli_bin
 20355-20368  _cscli_path
  6766-6791   _daily_summary_loop
 20386-20403  _darf_journal_lesen
  3064-3089   _darf_ytdlp_nachschlagen
 11815-11836  _dashboard_adresse
 20988-21011  _db_maintenance_loop
  6735-6763   _db_vacuum_loop
 16042-16066  _detect_foreign_ad
  1571-1582   _diag_path_owner
 17327-17372  _director_finalize
 18290-18297  _director_for
 17276-17324  _director_mark
 21908-21911  _disc_state_get
 21914-21921  _disc_state_set
 20916-20925  _discord_bot_starten
 20879-20890  _discord_einladung_merken
 20928-20932  _discord_invite
 20893-20913  _discord_kontext
 21869-21905  _discord_live_thread
 17479-17491  _discord_notify
 20851-20876  _discord_ops_alert
 21767-21865  _discord_post_user
 21511-21517  _discord_stop
  6794-6871   _disk_alarm_loop
 24360-24409  _disk_autoclean
 24583-24596  _disk_guard_loop
 13652-13659  _drossel_hoeher
 13648-13649  _drossel_stufe
 13662-13670  _drossel_zuruecksetzen
 11992-11994  _dump_all_threads
 10543-10606  _enrich_proxies_with_geo
  2150-2211   _ensure_cookie_file_netscape
  8824-8827   _ensure_notify_topic
 10787-10824  _ensure_proxy_ready
  8778-8805   _ensure_topic
   726-728    _env_int
   731-733    _env_int_range
 17524-17537  _event_webhook
 12670-12683  _evolution_loop
  5919-5953   _extract_file_payload
  2283-2285   _extract_urls_from_streamurl_node
 20371-20378  _f2b_sudo_hint
 25136-25199  _fatal_vom_botteil
 23999-24014  _fd_grenze_anheben
  4694-4704   _fehler_text
 10444-10462  _fetch_proxy_list
 18077-18105  _fetch_tiktok_room_id
   809-812    _ff_cmd
 13481-13486  _find_chromium
  3455-3457   _find_external_recorder
  2288-2290   _find_stream_urls
 12370-12395  _fire_webhooks
  7703-7712   _fork_safe
   915-928    _freeai_chat_sync_metered
 20417-20421  _geo_lookup_ips
  3727-3736   _get_ai_session
  7536-7576   _get_live_info
  2915-2922   _get_resolve_semaphore
  8028-8418   _handle_single_tracking
 24182-24184  _hb
 24187-24204  _hb_while
 12958-12960  _highlight_cfg
 12963-12992  _highlight_observe
 13489-13507  _htmlov_screenshot_cmd
 17783-17793  _httpx_proxy
 12403-12415  _in_quiet_hours
 24964-24975  _init_db_oder_abbruch
 25782-25813  _install_fast_eventloop
  9668-9722   _install_fast_json
 11997-12013  _install_faulthandler
 19033-19042  _intel_ensure_schema
 19085-19120  _intel_index_loop
 19054-19069  _intel_index_one
 19045-19051  _intel_semantic
  5219-5228   _is_authorized
  7914-7935   _is_dead
  2273-2275   _is_hevc
 20406-20408  _is_private_ip
  1790-1797   _is_process_running
  6507-6514   _is_quiet_hours
  1364-1373   _is_upload_window
  4559-4574   _iso
  9757-9770   _json_error_handler
  6729-6730   _kick_broadcaster_id
  6641-6683   _kick_follower_count
  6625-6628   _kick_slug
 11447-11454  _kick_user_token
  7835-7860   _kick_ws_pause
 24952-24961  _kickmod_boot
  4149-4152   _kind_from_filename
 12432-12434  _latest_popularity
  1727-1736   _laufstand
 24543-24580  _laufstand_loop
 24106-24144  _leistung_erheben
 18696-18745  _live_react_loop
 18363-18685  _live_react_worker
  3305-3417   _live_status_aufloesen
 16925-16936  _live_transcript_push
 18687-18694  _live_users
 17375-17419  _living_title_loop
 21154-21226  _local_backup_scan
  9739-9753   _log_5xx
 24147-24179  _log_schleuse_pruefen
   799-806    _log_sicher
 14076-14088  _looks_like_codec_err
 14071-14073  _looks_like_source_expired
  7753-7783   _loop_fehler
 12017-12026  _loop_heartbeat
 23905-23938  _loop_lag_monitor
 23952-23972  _loop_stockung_melden
 23975-23985  _loop_takt_starten
 12029-12102  _loop_watchdog_thread
 16802-16819  _loyalty_add
 16793-16799  _loyalty_get
 16822-16830  _loyalty_top
 12542-12544  _manual_donations_total
  4901-4920   _manual_status
  7937-7938   _mark_dead
 11063-11079  _marketing_loop
 22476-22494  _maybe_handle_command
 24682-24706  _maybe_hype_clip
 21561-21589  _meme_klassifizieren
  4056-4061   _migrate_columns
 22755-22766  _mod_is_exempt
 22769-22774  _mod_warn_first
 22777-22780  _mod_warn_text
 12727-12746  _modlog
 12710-12724  _modlog_schreiben
  1060-1062   _multistream_targets
  3092-3128   _nachschlag_ytdlp
  7715-7716   _nc_create_subprocess_exec
  7719-7720   _nc_create_subprocess_shell
 11384-11401  _news_loop
 12769-12771  _normalize_ingest
  2505-2522   _note_check_duration
  8818-8821   _notify_topic_name
  3131-3151   _ohne_url_melden
 16951-16959  _oracle_memories
 17225-17259  _oracle_memorize
 16962-16975  _oracle_persona
 16944-16948  _oracle_recent_text
 13115-13116  _ov_atomic_write
 13106-13108  _ov_bar
 15945-15957  _ov_clip_text
 13111-13112  _ov_oneline
 20083-20112  _overlay_push
 13435-13478  _overlay_render_size
 12838-12842  _overlay_session_reset
 20048-20050  _overlay_src_ok
 16029-16039  _own_invites
 13430-13432  _parse_size
 20600-20680  _parse_ssh_attacks
  7138-7171   _pause_resume_cmd
  2032-2076   _persist_refreshed_cookies
  1935-1967   _pick_checked_pull_proxy
  9841-9854   _pin_auth_value
  9900-9901   _pin_clear_fail
  9880-9883   _pin_locked
  9886-9897   _pin_note_fail
  9857-9877   _pin_ok
 19890-19915  _piper_pick_model
 19975-20026  _piper_say
 12332-12367  _post_json_threaded
 13409-13427  _probe_video_size
  1818-1835   _proc_is_recorder
 10756-10784  _proxy_pool_refresh_loop
  1901-1932   _proxy_report_recording
  8516-8554   _pruefstand_melden
 24034-24045  _pruefung_verworfen
 11982-11984  _prune_stall_dumps
 11133-11303  _public_stats
  2098-2104   _pull_proxy_still
 17495-17521  _push_notify
 10060-10062  _pwa_dir
 10513-10528  _quick_validate_proxy
 12398-12400  _quiet_hours_config
 10025-10058  _rate_guard
 16763-16769  _react_warn
  7623-7662   _reap_proc
  9052-9119   _rec_auto_abschalten
  8999-9049   _rec_frueh_getrennt
  8882-8944   _rec_kategorie_melden
  8947-8996   _rec_totstreak_fortschreiben
  2545-2567   _record_check_outcome
   794-796    _redact_stream_urls
 10683-10753  _refresh_proxy_pool
  2322-2413   _resolve_via_html
  2695-2892   _resolve_via_webcast_api_v2
  2955-3040   _resolve_via_ytdlp
 22085-22214  _resolve_youtube_ingest
  2299-2319   _resolver_stumm
 12821-12832  _restream_active_sources
 13758-13882  _restream_avatar_feeder_start
 13885-13894  _restream_avatar_feeder_stop
 18136-18254  _restream_chat_guardian
 12995-13067  _restream_chat_push
 13092-13101  _restream_chat_push_async
 13510-13619  _restream_html_overlay_start
 13622-13635  _restream_html_overlay_stop
 12780-12803  _restream_overlay_files
 18749-18781  _restream_platform_state
 18949-18984  _restream_resume_after_restart
 13942-14014  _restream_tts_enqueue_wav
 13371-13403  _restream_tts_feeder
 13368-13369  _restream_tts_fifo_path
 13897-13924  _restream_tts_start
 13926-13940  _restream_tts_stop
 18787-18946  _restream_verify_loop
 21119-21131  _retention_loop
 21113-21116  _retention_scan
  2652-2654   _room_is_abo
  5957-6074   _run_ai_call
 12125-12138  _run_async_from_flask
 20411-20414  _run_priv
 25770-25778  _run_selfcheck_and_exit
 21134-21145  _s3_client
  7964-8015   _safe_send
  4827-4843   _sample_net_throughput
  2597-2627   _schedule_next_check
 21067-21110  _scheduler_loop
  4064-4066   _schema_pk
 12142-12147  _scraper_session
 22783-22822  _screen_full
 11498-11535  _sec_headers
  2278-2280   _select_stream_from_data_section
 25490-25767  _selfcheck
  8830-8864   _send_live_notice
  1387-1391   _should_defer_upload
 21635-21671  _shrink_for_discord
 10065-10077  _sicheres_ziel
 20947-20985  _sicherheits_erinnerung_loop
 24603-24620  _sign_health_check
 24623-24642  _sign_health_loop
  4577-4602   _sitzung_bestimmen
  7732-7743   _spawn
 26195-26225  _spawn_from_flask
 24048-24054  _speicher_maps
 24057-24072  _speicher_pflegen
 17795-18074  _start_chat_listener
 24017-24031  _start_gesperrt
 12105-12122  _start_loop_watchdog
 11330-11379  _stats_loop
 11309-11312  _stats_output_path
 11315-11327  _stats_write
 19927-19941  _stimme_saubern
 19948-19972  _stimme_schon_gesagt
  8497-8513   _storage_cleanup_loop
 24662-24669  _story_for
  3480-3486   _stream_url_expiry
  3488-3493   _stream_url_ttl
 15992-15999  _streamer_persona_get
 21251-21403  _system_backup
 21412-21442  _system_backup_loop
 11942-11960  _task_auf_bot_schleife
 23596-23612  _telegram_befehlsmenue
  7786-7832   _telegram_polling_fehler
 10465-10504  _test_proxy
 11011-11027  _testpush_resolve_live
  7940-7961   _tg_sprache_setzen
  8737-8747   _tg_topics_load_into_mem
  8734-8735   _tg_topics_path
  8749-8756   _tg_topics_save
  9815-9823   _token_ok
  8759-8763   _topic_forget
 12418-12429  _tracking_max_duration
  4357-4371   _tracking_remove_cleanup
  4388-4400   _tracking_resume_cleanup
  1629-1652   _try_attach_file_handler
 19917-19925  _tts_cleanup
 10987-10991  _tunnel_effective
 24412-24432  _tunnel_lage
 24488-24540  _tunnel_wacht_loop
 19413-19466  _twitch_channel_status
 22825-22970  _twitch_chat_loop
 21927-21940  _twitch_clip_versuchen
 22639-22742  _twitch_eventsub_loop
  1410-1423   _upload_queue_add
  1434-1436   _upload_queue_count
  1393-1402   _upload_queue_load
  1383-1385   _upload_queue_path
  1425-1432   _upload_queue_remove
  1404-1408   _upload_queue_save
  1438-1479   _upload_window_loop
  7596-7603   _uptime_s
 12757-12766  _url_host
  3154-3253   _url_nachschlag
   875-879    _usage_record_claude
 24776-24798  _v37_pause_source
 24740-24750  _v37_restream_restart
 24753-24773  _v37_unpause_source
  7863-7907   _verbindung_verloren
  6686-6717   _viewer_sample_loop
  9904-9907   _wants_html
  7606-7620   _warn_empty_env
 24225-24346  _watchdog_loop
 22360-22368  _wchat_thank_ok
 17563-17593  _whisper_get_model
  7693-7700   _whisper_native_section
 16750-16756  _whisper_pool
 17687-17719  _whisper_segments
 17595-17611  _whisper_stumm
 17614-17684  _whisper_transcribe
 13163-13325  _write_restream_overlay
 13125-13160  _write_restream_overlay_async
 22994-23090  _youtube_api_chat_loop
 19469-19572  _youtube_api_status
 19575-19642  _youtube_channel_status
 23093-23254  _youtube_chat_loop
 21943-21968  _youtube_clip_versuchen
 22220-22233  _youtube_restream_autoconfig
 22236-22260  _youtube_restream_autoconfig_inner
 22327-22355  _youtube_send
 19710-19751  _youtube_set_channel
 22263-22297  _yt_access_token
 22300-22315  _yt_live_chat_id
 22323-22324  _yt_sendrate_cfg
 22973-22988  _yt_timeout
  2939-2940   _ytdlp_detect_available
  2942-2953   _ytdlp_note_result
 11987-11989  _zombie_child_count
 24090-24103  _zustand_kennzahlen
  7472-7496   about
  4268-4272   add_ai_log_entry
  4185-4188   add_archive_entry
  4865-4867   add_archive_rule
  4605-4676   add_recording
  4332-4349   add_tracking
  6077-6110   ai
  3879-3960   ai_chat
  3994-4004   ai_history_append
  4006-4011   ai_history_clear
  3983-3992   ai_history_load
  3968-3981   ai_rate_limit_check
  6139-6147   aireset
 17092-17111  azrael_chat
 23259-23381  brain_cmd
  3496-3501   build_recording_cmd
  4352-4355   bulk_add_trackings
  6940-6999   bulkadd
  8557-8717   check_all_trackings
  4404-4416   claim_live_transition
 16069-16682  class KickModerator
 14091-15832  class RestreamManager
 10870-10912  classify_proxy_anonymity
  6185-6383   cleanup
  5155-5161   cleanup_old_recordings
  4550-4557   clear_recording
 21971-22042  clip_moment
  4817-4820   compute_storage_forecast
  7062-7135   cookies_cmd
  4323-4329   count_trackings_for_chat
  4255-4266   decide_preferred_recorder
  4195-4198   delete_archive_entry
  4869-4871   delete_archive_rule
  5614-5761   diag
 23493-23554  einnahmen_cmd
  4811-4814   find_recordings_by_fingerprint
  4216-4232   finish_recording_attempt
  4376-4378   get_all_active_trackings
  4283-4285   get_all_checks
  4678-4681   get_all_recordings
  4760-4762   get_all_tags_with_counts
  4788-4791   get_annotations_for_recording
  4190-4193   get_archive_entry
  4781-4784   get_bookmarked_recordings
  2138-2143   get_cookie_health
  4748-4754   get_event_log
  4239-4253   get_last_recording_attempt
  3256-3298   get_live_status
  5094-5097   get_manual_recordings
  4796-4799   get_or_compute_inspect_sync
  5196-5199   get_outcome_breakdown
  4767-4770   get_priority_poll_interval
  4234-4237   get_recent_recording_attempts
  4683-4686   get_recording_by_id
  4774-4777   get_recording_note
  3667-3696   get_redis
  4312-4315   get_stats
  5149-5153   get_storage_stats
  4889-4891   get_tiktok_status_distribution
  4418-4427   get_tracking_state
  4373-4374   get_trackings_for_group
  5110-5113   get_trash_recordings
  9179-9647   handle_recording_finished
 23588-23593  hilfe_cmd
  4079-4140   init_db
  4861-4863   list_archive_rules
  5399-5437   live
  8018-8026   live_check_worker
  3751-3790   llm_chat
  3813-3843   llm_chat_sync
  3798-3810   llm_list_models
  4707-4740   log_event
  1752-1785   log_recording_failure
  7285-7334   logs_cmd
 25202-25480  main
  6113-6136   on_ai_media
  7411-7437   on_ai_reply
  7440-7469   on_azrael_mention
  7501-7531   on_callback
 17117-17222  oracle_handle
  7174-7177   pause_tracking
  5209-5214   profile_keyboard
  5352-5396   quelle
  7236-7282   quota
  8420-8494   reaper_loop
  4885-4887   record_tiktok_status
  6152-6182   recstatus
  3698-3706   redis_get_json
  3709-3715   redis_set_json
 23615-23625  report_cmd
 10915-10917  report_proxy_result
  2416-2458   resolve_tiktok_live_stream
  5105-5108   restore_recording
  7180-7183   resume_tracking
  4874-4879   run_archive_rules
 23628-23885  run_bot
 11839-11933  run_flask
  4849-4852   sample_bandwidth_for_active
  4275-4281   save_tiktok_check
  4542-4548   set_recording_file
  4381-4385   set_tracking_paused
  5100-5103   soft_delete_recording
  8870-8880   split_and_send_video
  5262-5304   start
  4200-4214   start_recording_attempt
  6386-6424   stats
  5039-5092   stop_manual_recording
  7186-7233   stoprec
  6610-6618   summary_cmd
  7337-7408   sysres
  5763-5907   teststream
  5306-5347   tiktok
  7002-7059   topusers
  5474-5531   track
  5439-5471   track_exact
  5545-5612   tracklist
  4923-5037   trigger_manual_recording
  4503-4540   try_acquire_recording_lock
  5116-5118   universal_search
 23557-23585  unpause_cmd
  5533-5543   untrack
 23384-23490  update_cmd
  4806-4809   update_recording_fingerprint
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
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
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
